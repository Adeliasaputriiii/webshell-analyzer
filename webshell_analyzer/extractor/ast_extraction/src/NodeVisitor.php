<?php

namespace NodeVisitor;

require_once __DIR__ . '/../vendor/autoload.php';
require_once __DIR__ . '/featuresDeclare.php';

use Features\featureWrapper;
use PhpParser\NodeVisitorAbstract;
use PhpParser\Node;
use PhpParser\Node\Name;
use PhpParser\Node\Expr;
use PhpParser\Node\Stmt;
use PhpParser\Node\Scalar;


class NodeVisitor extends NodeVisitorAbstract {
    private featureWrapper $features;
    private array $superglobal = ['_GET', '_POST', '_COOKIE', '_REQUEST', '_FILES', '_ENV', '_SERVER', '_SESSION', 'GLOBALS'];
    private array $decodeFunctions = ['base64_decode', 'gzinflate', 'gzuncompress', 'str_rot13'];

    private array $varsFromDecode = [];

     public function __construct(featureWrapper $features){
        $this->features = $features;
    }

    public function enterNode(Node $node) {
        $this->handleDynamicFeatures($node);
        $this->handleStructuralFeatures($node);
    }
    

    private function getFuncName(Node $node): ?string {
        if($node instanceof Expr\FuncCall && $node->name instanceof Name){
            if($node->name instanceof Name){
                return strtolower($node->name->toString());
            }
        }
        return null;
    }


    private function isSuperglobal(Node $node): bool {
        return $node instanceof Expr\ArrayDimFetch && $node->var instanceof Expr\Variable && is_string($node->var->name) && in_array($node->var->name, $this->superglobal);
    }

    private function isDecodeFunction(Node $node): bool {
        if($node instanceof Expr\FuncCall && $node->name instanceof Name){
            $fname = $this->getFuncName($node);
            return in_array($fname, $this->decodeFunctions);
        }
        return false;
    }
    

    private function handleDynamicFeatures(Node $node){
        #check for variable variables (varExists feature)
        if($node instanceof Expr\Variable && $node->name instanceof Expr\Variable){
            $this->features->dynamicFeatures->varExists = true;
        }

        if($node instanceof Expr\Variable){
            $this->features->dynamicFeatures->varUsageCount++;
        }

        if($node instanceof Expr\Assign){
            $this->features->dynamicFeatures->assignmentCount++;

            if($node->expr instanceof Expr\FuncCall && $this->isDecodeFunction($node->expr)){
                if($node->var  instanceof Expr\Variable && is_string($node->var->name)){
                    $this->varsFromDecode[$node->var->name] = true;
                }
            }
        }
    }

    private function handleStructuralFeatures(Node $node) {

        #class definition exists (classDefExists feature)
        if($node instanceof Stmt\Class_){
            $this->features->structuralFeatures->classDefExists = true;
        }

        #count function definitions (funcDefCount feature)
        if($node instanceof Stmt\Function_ || $node instanceof Stmt\ClassMethod){
            $this->features->structuralFeatures->funcDefCount++;
        }

        #count superglobal used as function argument (superglobalAsFuncArg feature)
        if($node instanceof Expr\FuncCall ){
            foreach($node->args as $arg){
                if($this->isSuperglobal($arg->value)){
                    $this->features->structuralFeatures->superglobalAsFuncArg++;
                }
            }
        }


        if($node instanceof Expr\BinaryOp\Concat){
            $this->features->structuralFeatures->suspiciousConcat = ($this->features->structuralFeatures->suspiciousConcat ?? 0) + 1;
        }
    }
}
?>