<?php

namespace Features;

class dynamicFeatures{
    public bool $dynamicFuncCallExists = false;
    public bool $varExists = false;
    public int $varUsageCount = 0;
    public int $assignmentCount = 0;
}

class structuralFeatures{
    public bool $classDefExists = false;
    public int $funcDefCount = 0;
    public int $superglobalAsFuncArg = 0;
    public int $suspiciousConcat = 0;
}

class featureWrapper{
    public dynamicFeatures $dynamicFeatures;
    public structuralFeatures $structuralFeatures;

    public function __construct(){
        $this->dynamicFeatures = new dynamicFeatures();
        $this->structuralFeatures = new structuralFeatures();
    }

    public function toArray(): array {
        return array_merge(
           get_object_vars($this->dynamicFeatures),
           get_object_vars($this->structuralFeatures)
        );
    }
}

?>
